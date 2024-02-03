import React from "react";
import ReactDOM from "react-dom/client";
import {
  RouterProvider,
  createRoute,
  createRouter,
} from "@tanstack/react-router";
import { NextUIProvider } from "@nextui-org/react";
import "./index.css";
import { rootRoute } from "./routes/__root";
import Home from "./routes/Home";

const aboutRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/about",
  component: function About() {
    return <div className="p-2">Hello from About!</div>;
  },
});

const homeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: Home,
});

const routeTree = rootRoute.addChildren([homeRoute, aboutRoute]);

const router = createRouter({ routeTree, defaultPreload: "intent" });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <NextUIProvider>
      <RouterProvider router={router} />
    </NextUIProvider>
  </React.StrictMode>
);
