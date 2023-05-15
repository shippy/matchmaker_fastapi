/// <reference types="vite/client" />

// https://stackoverflow.com/a/73557254/2114580
declare module '*.vue' {
    import type { DefineComponent } from 'vue';
    const component: DefineComponent<{}, {}, any>;
    export default component;
}
  