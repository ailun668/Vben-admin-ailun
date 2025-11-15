# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Vue 3 + TypeScript + Vite** admin dashboard application with:
- Role-based access control (RBAC) system
- Dynamic routing based on user permissions
- Mock API backend using vite-plugin-mock
- Ant Design Vue UI components
- Pinia state management with persistence
- Full TypeScript support

## Quick Start

### Installation & Development
```bash
# Install dependencies
npm install
# or
pnpm install

# Start development server
npm run dev
# or
pnpm dev

# Build for production
npm run build

# Type checking
vue-tsc -b

# Preview production build
npm run preview
```

Development server runs at `http://localhost:5173`

### Test Credentials
- **Admin**: username `admin`, password `admin123` (full access)
- **User**: username `user`, password `user123` (limited access to Home and Settings)

## Architecture & Key Concepts

### Directory Structure
```
src/
├── router/index.ts              # Route configuration + guards
├── store/modules/
│   ├── user.ts                  # User auth state + token persistence
│   ├── permission.ts            # Role-based route generation
│   └── app.ts                   # General app state
├── api/
│   ├── http.ts                  # Axios client with interceptors
│   ├── user.ts                  # User API calls
│   └── types.ts                 # TypeScript type definitions
├── views/
│   ├── LoginView.vue            # Login page
│   ├── HomeView.vue             # Dashboard home
│   ├── DashboardView.vue        # Analytics dashboard
│   ├── UsersView/
│   │   ├── UsersView.vue        # User management (table + CRUD)
│   │   └── AddUserModal.vue     # Add user modal
│   ├── RolesView.vue            # Role management
│   ├── PermissionsView.vue      # Permission management
│   └── SettingsView.vue         # Settings page
├── components/
│   └── Crud/                    # Reusable CRUD components
├── mock/user.ts                 # Mock API endpoints
└── main.ts                      # App entry point
```

### State Management (Pinia)

#### `store/modules/user.ts`
- **State**: `token`, `userInfo`, `loading`
- **Key Actions**:
  - `login(credentials)` - Authenticate and store token/user data
  - `getCurrentUser()` - Fetch current user info (called by route guard)
  - `logout()` - Clear auth state
  - `hasRole(role)` - Check if user has role
- **Persistence**: token and userInfo are auto-saved to localStorage via pinia-plugin-persistedstate

#### `store/modules/permission.ts`
- **Key Actions**:
  - `generateRoutes(roles)` - Filter routes based on user roles
  - `filterRoutes(routes, roles)` - Recursive route filtering logic
- **Computed**: `accessibleRoutes` - Returns routes for menu rendering

### Routing & Authentication

#### How It Works
1. **Route Guard** (`router/beforeEach` in `router/index.ts`):
   - Redirects unauthenticated users to `/login`
   - Checks user token and permissions on protected routes
   - Dynamically adds async routes based on user roles (only once via `isRouteAdded` flag)
   - Validates role access before allowing navigation

2. **Dynamic Routes** (`asyncRoutes` in `router/index.ts`):
   - All protected routes defined statically with `roles` metadata
   - Added dynamically to router only after auth confirmation
   - 404 fallback route added last

3. **Route Metadata**:
   - `title`: Display name for menus/breadcrumbs
   - `requiresAuth`: Whether authentication is required
   - `roles`: Array of role strings allowed to access (e.g., `['admin']`)

#### Critical Implementation Detail
- **`isRouteAdded` flag** prevents duplicate route registration on multiple guard calls
- **`getCurrentUser()`** is called during first navigation after login to fetch user info
- **Route re-navigation** (`next({...to, replace: true})`) occurs after routes are added so Vue Router picks them up

### API Integration

#### HTTP Client (`api/http.ts`)
- **Base URL**: `import.meta.env.VITE_API_BASE_URL` or `/api`
- **Request Interceptor**: Adds `Authorization: Bearer {token}` header
- **Response Interceptor**:
  - Checks `code === 0` for success (custom business logic)
  - Handles `code === 401` by logging out and redirecting to login
  - Maps HTTP errors (400, 403, 404, 500) to messages

#### Mock API (`src/mock/user.ts`)
- Intercepts requests matching patterns (e.g., `/api/user/login`)
- Validates credentials and returns mock tokens
- Endpoints:
  - `POST /api/user/login` - Login with username/password
  - `GET /api/user/info` - Get current user (requires valid token in header)
  - `POST /api/user/logout` - Logout
  - `GET /api/user/list` - Get paginated user list with search/filter

### TypeScript Configuration
- **Base path alias**: `@/` maps to `src/`
- **Type files**: `tsconfig.app.json` includes Vue and Node types
- Strict mode enabled - all code should be properly typed

## Common Development Tasks

### Adding a New Protected Route
1. Add route to `asyncRoutes` in `router/index.ts` with `roles` metadata:
   ```typescript
   {
     path: '/reports',
     name: 'reports',
     component: () => import('@/views/ReportsView.vue'),
     meta: {
       title: '报表',
       requiresAuth: true,
       roles: ['admin', 'manager']  // Who can access
     }
   }
   ```
2. Create the Vue component in `src/views/ReportsView.vue`
3. Menu auto-updates in `App.vue` - no other changes needed

### Extending Mock API
1. Add new mock handler to `src/mock/user.ts`:
   ```typescript
   {
     url: '/api/reports/data',
     method: 'get',
     response: ({ headers }) => {
       // Access token from headers.authorization if needed
       return {
         code: 0,
         data: [...],
         message: 'Success'
       }
     }
   }
   ```

### Checking User Permissions in Components
```vue
<script setup lang="ts">
import { useUserStore } from '@/store/modules/user'

const userStore = useUserStore()

// Check role
if (userStore.hasRole('admin')) {
  // show admin features
}

// Check permission
if (userStore.hasPermission('system:user:delete')) {
  // show delete button
}
</script>
```

## Known Limitations & To-Do

### Current Issues
- **localStorage persistence**: Implemented via pinia-plugin-persistedstate. Page refresh maintains login state.
- **No real API**: Currently uses vite-plugin-mock for all endpoints. To integrate real backend:
  1. Update environment variables for `VITE_API_BASE_URL`
  2. Modify mock endpoints in `src/mock/user.ts`

### Recommended Next Steps
- [ ] Add route transition animations
- [ ] Implement 403/404 error pages
- [ ] Add form validation to login page
- [ ] Add loading indicators during async operations
- [ ] Implement breadcrumb navigation
- [ ] Add internationalization (i18n) support

## Important Files & Their Purpose

| File | Purpose |
|------|---------|
| `router/index.ts` | **Core auth logic** - route guards, permission checking, dynamic route registration |
| `store/modules/user.ts` | **Auth state** - token, user info, login/logout/getCurrentUser actions |
| `store/modules/permission.ts` | **Route filtering** - generates accessible routes based on user roles |
| `api/http.ts` | **API setup** - Axios instance with auth token injection and error handling |
| `src/mock/user.ts` | **Mock backend** - all API endpoints for development |
| `App.vue` | **Layout** - dynamic menu rendering based on accessible routes |
| `vite.config.ts` | **Build config** - vite-plugin-mock setup, path aliases |

## Debugging Tips

### Check Auth State
Open browser DevTools → Application → Local Storage → `user_store` to see persisted token/userInfo

### Check Route Access
In router/index.ts route guard, accessible routes are computed from `permissionStore.accessibleRoutes`

### Mock API Issues
If API calls fail, check:
1. Network tab in DevTools - should show requests to `/api/*`
2. Mock response format must match `ApiResponse<T>` type (code, data, message)
3. Token validation in mock handlers compares `headers.authorization` with stored tokens

### Type Errors
Run `vue-tsc -b` to catch TypeScript errors during development

---

**Last Updated**: 2025-11-15
