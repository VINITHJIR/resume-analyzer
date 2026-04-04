import { useState } from "react";
import { registerUser } from "../services/auth";

function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    phone: ""
  });

  const handleRegister = async () => {
    try {
      await registerUser(form);
      alert("Registered successfully!");
      window.location.href = "/";
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <div className="flex h-screen justify-center items-center">
      <div className="bg-white p-6 shadow rounded w-80">
        <h2 className="text-xl mb-4 text-center">Register</h2>

        <input
          placeholder="Username"
          className="border p-2 mb-2 w-full"
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />

        <input
          placeholder="Email"
          className="border p-2 mb-2 w-full"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          type="password"
          placeholder="Password"
          className="border p-2 mb-2 w-full"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <input
          placeholder="Phone"
          className="border p-2 mb-4 w-full"
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />

        <button
          onClick={handleRegister}
          className="bg-green-500 text-white p-2 w-full"
        >
          Register
        </button>

        <p className="mt-3 text-sm text-center">
          Already have account?{" "}
          <span
            className="text-blue-500 cursor-pointer"
            onClick={() => (window.location.href = "/")}
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}

export default Register;