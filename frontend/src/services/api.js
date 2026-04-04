import axios from "axios";

const API = "http://127.0.0.1:8000";

// 🔥 ADD THIS (missing function)
export const analyzeResume = async (file) => {
  const token = localStorage.getItem("token");

  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(`${API}/upload`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`
    }
  });

  return res.data;
};

// existing
export const getResumes = async () => {
  const token = localStorage.getItem("token");

  const res = await axios.get(`${API}/my-resumes`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return res.data;
};