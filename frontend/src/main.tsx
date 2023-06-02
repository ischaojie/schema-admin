import "vite/modulepreload-polyfill";
import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Root, { loader as rootLoader } from "./routes/root.tsx";
import Index from "./routes/index";
import Model, { loader as modelLoader } from "./routes/model.tsx";
import { loader as indexLoader } from "./routes/index.tsx";
import ErrorPage from "./404.tsx";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import "virtual:uno.css";

library.add(fas);

const router = createBrowserRouter([
  {
    path: "/congers",
    element: <Root />,
    errorElement: <ErrorPage />,
    loader: rootLoader,
    children: [
      {
        index: true,
        element: <Index />,
        loader: indexLoader,
      },
      {
        path: "models/:modelId",
        element: <Model />,
        loader: modelLoader,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
