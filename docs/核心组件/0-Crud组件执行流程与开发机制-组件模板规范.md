# AI-Powered Crud Component: Development Specification

## 1. Overview

This document provides a comprehensive guide for developing features using the configuration-driven `Crud` component. Adhering to this specification will ensure consistency, maintainability, and allow AI assistants to understand and assist with development tasks effectively.

## 2. Core Concept: Configuration-Driven UI

The `Crud` component is designed to be entirely controlled by a single configuration object, `LocalCrudConfig`. Instead of writing imperative code to define UI and behavior, you declare it in this object.

**Golden Rule**: **Everything is configuration.** Avoid hard-coding business logic directly in the template. The configuration object is the single source of truth.

## 3. The `LocalCrudConfig` Object

This is the main object you will work with. It defines everything from the table columns to the actions in the toolbar.

```typescript
import type { LocalCrudConfig } from '@/components/Crud';

const partnerMarkupConfig: LocalCrudConfig = {
  // Basic page settings
  title: 'Partner Markup',
  pageConfig: {
    enableSearch: true,
    enableToolbar: true,
    enablePagination: true,
  },
  // API endpoint for the list
  api: '/pnapi/markups/merchants/',

  // All other options
  options: {
    // Search form definition
    formOptions: { /* ... */ },
    // Toolbar buttons definition
    toolbarActions: [ /* ... */ ],
    // Grid (table) definition
    gridOptions: { /* ... */ },
  },
};
```

## 4. Standard Development Workflow

### Step 1: Define a Shared Form Schema

For any resource, the "Add" and "Edit" forms are usually very similar. To avoid code duplication, define a single, shared `schema` array.

**Best Practice**: Include the `id` field in the shared schema and set it to `disabled: true`. This allows the same schema to be used for both editing (where the ID is displayed) and adding (where it is ignored).

**Example**: `markupFormSchema`

```typescript
const markupFormSchema = [
  {
    fieldName: 'id',
    component: 'Input',
    label: 'Markup ID',
    componentProps: {
      disabled: true, // Always disabled
      placeholder: 'Auto-generated ID',
    },
  },
  {
    fieldName: 'payment_product_name',
    component: 'Select',
    label: 'Payment Product Name',
    rules: 'required',
    // ... other fields
  },
  // ... more fields
];
```

### Step 2: Configure the "Edit" Action

The "Edit" action should be configured within the `actions` array of a column in `gridOptions`.

**Key Implementation Points**:

1.  **Use the Shared Schema**: Pass the `markupFormSchema` directly to the `formProps.schema`.
2.  **Use `apiConfig` (Crucial!)**: Define the `PATCH` endpoint using `apiConfig`. The `{id}` placeholder will be automatically replaced with the current row's ID. **Do not use the `api` function**, as it conflicts with the component's internal mechanisms.
3.  **Handle Data Transformation in Hooks**:
    *   `onOpened`: Use this hook to transform data coming **from the backend to the form**. For example, convert date strings to `dayjs` objects for the `DatePicker`.
    *   `beforeSubmit`: Use this hook to transform data going **from the form to the backend**. For example, convert `dayjs` objects back to ISO strings and numbers to strings if required by the API.

**Example**: "Edit" Action Configuration

```typescript
// Inside gridOptions.columns
{
  field: 'action',
  title: 'Actions',
  slots: { default: 'table-actions' },
  actions: [
    {
      label: 'Edit',
      component: 'Button',
      useFormModal: true,
      formProps: {
        // 1. Use the shared schema
        schema: [...markupFormSchema],
      },
      // 2. Use apiConfig for the PATCH request
      apiConfig: {
        url: '/pnapi/markups/merchants/{merchant_id}/{id}',
        method: 'PATCH',
      },
      // 3. Use hooks for data transformation
      hooks: {
        onOpened: ({ context, instance }) => {
          const data = { ...context };
          // string -> dayjs
          if (data.effective_from) {
            data.effective_from = dayjs(data.effective_from);
          }
          instance.setValues(data);
        },
        beforeSubmit: (values) => {
          // dayjs -> ISO string, number -> string
          return {
            effective_from: values.effective_from ? new Date(values.effective_from).toISOString() : null,
            payin_fee_fixed: String(values.payin_fee_fixed),
            // ... other transformations
          };
        },
        onSubmitSuccess: () => {
          message.success('Update successful');
          refresh(); // Refresh the grid
        },
      },
    },
  ],
}
```

### Step 3: Configure the "Add" Action

The "Add" action is typically handled by a button in the `toolbarActions` that opens a separate modal component.

**Key Implementation Points**:

1.  **Create a Separate Modal Component**: Create a new `.vue` file (e.g., `AddMarkupModal.vue`). This component will contain its own form logic.
2.  **Reuse the Shared Schema**: Inside the modal, import and use the `markupFormSchema`. You can filter out the `id` field since it's not needed for creation.
3.  **Handle Submission Manually**: The modal is responsible for its own form validation and API `POST` request.
4.  **Emit Events**: The modal should emit `success` or `cancel` events to communicate the result back to the parent page.

**Example**: Toolbar Configuration

```typescript
// Inside options.toolbarActions
[
  {
    label: 'ADD Product',
    component: 'Button',
    componentProps: { type: 'primary' },
    // Simply opens the modal
    onClick: openAddMarkupModal,
  },
]
```

**Parent Page Logic**:

```vue
<script setup>
import AddMarkupModal from './AddMarkupModal.vue';

const addMarkupModalVisible = ref(false);

const openAddMarkupModal = () => {
  addMarkupModalVisible.value = true;
};

const handleAddMarkupSuccess = () => {
  addMarkupModalVisible.value = false;
  crudRef.value?.reload(); // Refresh the grid
};
</script>

<template>
  <Crud :config="partnerMarkupConfig" ref="crudRef" />
  <AddMarkupModal
    v-if="addMarkupModalVisible"
    :open="addMarkupModalVisible"
    @cancel="addMarkupModalVisible = false"
    @success="handleAddMarkupSuccess"
  />
</template>
```

## 5. Grid (Table) Best Practices

To ensure consistency and avoid common layout issues with `VxeGrid`, please follow these guidelines.

### 5.1. Column Definition

- **Field Path**: The `field` property supports dot notation for nested data. Ensure it correctly maps to the backend data structure (e.g., `field: 'kyc.partner_name'`).
- **Responsive Width**: Use `minWidth` instead of a fixed `width` for columns. In conjunction with the grid-level `fit: true` option, this allows the table to adapt gracefully to different screen sizes.

```typescript
// Inside gridOptions
{
  fit: true, // Make sure this is enabled at the grid level
  columns: [
    {
      field: 'kyc.partner_name',
      title: 'Partner Name',
      minWidth: 220, // Use minWidth for responsive behavior
      showOverflow: 'ellipsis',
    },
    // ... other columns
  ],
}
```

### 5.2. Fixing Alignment Issues with Scoped CSS

The `VxeGrid` component can sometimes have header and cell alignment issues. To resolve this, add the following standard CSS block to your component's `<style scoped>` section. This is the standard solution for this project.

```css
/* Standard CSS for VxeGrid Alignment Fix */
:deep(.vxe-table--main-wrapper table) {
  width: 100% !important;
  table-layout: fixed !important;
}

:deep(.vxe-table--header-wrapper),
:deep(.vxe-table--body-wrapper) {
  width: 100% !important;
}

:deep(.vxe-header--row) th,
:deep(.vxe-body--row) td {
  padding: 8px 16px !important;
  text-align: center !important;
}

:deep(.vxe-header--column),
:deep(.vxe-body--column) {
  box-sizing: border-box;
  height: 48px;
}

:deep(.vxe-cell) {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
}

:deep(.vxe-cell--title) {
  display: inline-flex !important;
  justify-content: center !important;
  width: 100% !important;
}
```

## 6. Data Transformation Cheatsheet

| Field Type | Backend Format | Form Display Format | Transformation Hook | Direction | Code Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Date** | ISO String | `dayjs` object | `onOpened` | Backend → Form | `data.field = dayjs(data.field);` |
| **Date** | `dayjs` object | ISO String | `beforeSubmit` | Form → Backend | `values.field.toISOString()` |
| **Number** | String | Number | `beforeSubmit` | Form → Backend | `String(values.field)` |

## 7. Conclusion

By following this configuration-driven approach, you create predictable, maintainable, and scalable UI. This strict adherence to convention allows both human developers and AI assistants to easily understand, debug, and extend the functionality of any `Crud` page.
 