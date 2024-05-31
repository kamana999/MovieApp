import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { useAuth } from "../provider/authProvider";
import ProtectedRoute from "./ProtectedRoute";
import MovieList from "../components/MoviesList";
import UploadCsv from "../components/UploadCsv";
import Login from "../components/Login";


const Routes = () => {
    const { token } = useAuth();
    // Route configurations go here

    const routesForPublic = [
        {
          path: "/login",
          element: <Login />,
        },
      ];

    const routesForAuthenticatedOnly = [
        {
            path: "/",
            element: <ProtectedRoute />,
            children: [
              {
                path: "/movie_list",
                element: <MovieList />,
              },
              {
                path: "/upload",
                element: <UploadCsv />,
              }
            ],
          },
      ];

    const routesForNotAuthenticatedOnly = [
        {
            path: "/login",
            element: <Login />,
        },
    ];
    const router = createBrowserRouter([
        ...routesForPublic,
        ...(!token ? routesForNotAuthenticatedOnly : []),
        ...routesForAuthenticatedOnly,
      ]);
    return <RouterProvider router={router} />;
};

export default Routes;