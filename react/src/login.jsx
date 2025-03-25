/* eslint-disable */
import React from "react";
import { GoogleLogin } from "@react-oauth/google";

const Login = () => {
    const handleSuccess = async (response) => {
        try {
            const googleToken = response.credential;

            const res = await fetch("http://127.0.0.1:8000/api/auth/google/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token: googleToken }),
            });

            if (!res.ok) {
                throw new Error("Failed to authenticate");
            }

            const data = await res.json();
            console.log("JWT Token:", data.access);

            localStorage.setItem("access_token", data.access);
            localStorage.setItem("refresh_token", data.refresh); // Store refresh token too
        } catch (error) {
            console.error("Login failed:", error);
        }
    };
    const refreshAccessToken = async () => {
        const refreshToken = localStorage.getItem("refresh_token");

        if (!refreshToken) {
            console.log("No refresh token found. User must log in again.");
            return null;
        }

        try {
            const res = await fetch("http://127.0.0.1:8000/api/auth/token/refresh/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ refresh: refreshToken }),
            });

            if (!res.ok) {
                console.log("Failed to refresh token. User must log in again.");
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                return null;
            }

            const data = await res.json();
            localStorage.setItem("access_token", data.access);
            return data.access;
        } catch (error) {
            console.error("Error refreshing token:", error);
            return null;
        }
    };




    return (
        <div>
            <h2>Login with Google</h2>
            <GoogleLogin onSuccess={handleSuccess} onError={() => console.log("Login Failed")} />
        </div>
    );
};

export default Login;
