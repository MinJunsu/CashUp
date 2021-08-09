import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getProgressData = () => api.get("/data/progress/");
// export const getSimulateData = (data) => api.post("/simulate/", data);
export const getSimulateData = (data) => api.post("/simulate/", data);