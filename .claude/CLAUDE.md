# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Vue 3 + TypeScript + Vite project using Ant Design Vue for UI components. The application has a basic layout with a sidebar, header, and content area, displaying user information fetched from a mock API.

## Tech Stack

- **Framework**: Vue 3 (Composition API with `<script setup>`)
- **Language**: TypeScript 5.9
- **Build Tool**: Vite 7.2
- **State Management**: Pinia 3.0 (with persistence plugin)
- **UI Library**: Ant Design Vue 4.2
- **Icons**: @ant-design/icons-vue
- **HTTP Client**: axios
- **Mocking**: vite-plugin-mock (for development API mocking)
- **Routing**: Vue Router 4.6
- **Utilities**: lodash-es, dayjs, crypto-js, nprogress, qs

## Project Structure

```
src/
  ├── api/           # API service layer (currently empty, ready for implementation)
  ├── assets/        # Static assets
  ├── components/    # Reusable Vue components
  ├── mock/          # Mock API responses for development
  ├── router/        # Vue Router configuration
  ├── store/         # Pinia stores (currently empty, ready for implementation)
  ├── views/         # Page components
  ├── App.vue        # Root component with Ant Design layout
  └── main.ts        # Application entry point
```

## Common Commands

### Development
- `npm run dev` - Start Vite dev server with HMR
- `npm run build` - Build for production (includes TypeScript check)
- `npm run preview` - Preview production build locally

## Code Style & Architecture

### Vue Components
- Use `<script setup>` syntax for all components
- Organize template, script, and style in order
- Component names should be PascalCase (e.g., `UserCard.vue`)

### TypeScript
- Strict mode enabled (`strict: true`)
- No unused locals/parameters enforced
- Type all reactive values and function parameters
- Use proper typing for props: `defineProps<{ key: Type }>()`

### State Management (Pinia)
- Create stores in `src/store/` directory
- Use composition-style store definitions with `defineStore`
- Leverage pinia-plugin-persistedstate for localStorage persistence

### API Layer
- Mock APIs are in `src/mock/` (using vite-plugin-mock)
- Create API service functions in `src/api/` directory
- Use axios for HTTP requests with base configuration

### Styling
- Use scoped styles in SFC `<style scoped>` blocks
- Ant Design Vue classes are available globally
- CSS is pre-configured to work with Ant Design reset

## Mock API Setup

Mock API endpoints are defined in `src/mock/` using vite-plugin-mock:
- `GET /api/user` - Returns user profile data
- Add new mock endpoints by creating files in `src/mock/` following the MockMethod pattern

Example mock endpoint:
```typescript
export default [
  {
    url: '/api/endpoint',
    method: 'get|post|put|delete',
    response: () => ({ /* response data */ })
  }
] as MockMethod[];
```

## TypeScript Configuration

- Base config extends `@vue/tsconfig/tsconfig.dom.json`
- DOM libraries included
- Vite client types available via `vite/client`
- Build info stored in `node_modules/.tmp/tsconfig.app.tsbuildinfo`

## Development Notes

- Ant Design Vue CSS reset is imported in `main.ts`
- Application mounts to `#app` element in `index.html`
- HMR (Hot Module Replacement) enabled by default with Vite
- Vue 3 Composition API fully supported
- Router uses web history mode (not hash mode)
