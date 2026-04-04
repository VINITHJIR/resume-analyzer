

import axios from "axios";

const API = "http://127.0.0.1:8000";

export const registerUser = async (data) => {
  return axios.post(`${API}/auth/register`, data);
};

export const loginUser = async (data) => {
  const res = await axios.post(`${API}/auth/login`, data);
  return res.data;
};