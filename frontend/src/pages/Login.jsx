import { useState } from "react";
import { loginUser } from "../services/auth";

function Login() {
  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");

    // 🔴 Validation
    if (!form.username || !form.password) {
      setError("Username and Password are required");
      return;
    }

    try {
      const res = await loginUser(form);

      // 🔴 Check token exists
      if (!res.token) {
        setError("Invalid credentials");
        return;
      }

      // ✅ Save token
      localStorage.setItem("token", res.token);

      // ✅ Redirect
      window.location.href = "/dashboard";

    } catch (err) {
      setError("Login failed. Check username/password");
    }
  };

  return (
    <div className="flex h-screen justify-center items-center">
      <div className="bg-white p-6 shadow rounded w-80">
        <h2 className="text-xl mb-4 text-center">Login</h2>

        {/* 🔥 Error message */}
        {error && (
          <p className="text-red-500 text-sm mb-2">{error}</p>
        )}

        <input
          placeholder="Username"
          value={form.username}
          onChange={(e) =>
            setForm({ ...form, username: e.target.value })
          }
          className="border p-2 mb-2 w-full"
        />

        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
          className="border p-2 mb-2 w-full"
        />

        <button
          onClick={handleLogin}
          className="bg-blue-500 text-white p-2 w-full"
        >
          Login
        </button>

        <p className="mt-3 text-sm text-center">
          Don't have account?{" "}
          <span
            className="text-blue-500 cursor-pointer"
            onClick={() => (window.location.href = "/register")}
          >
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

export default Login;