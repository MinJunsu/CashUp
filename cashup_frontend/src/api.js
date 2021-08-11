import axios from "axios";

const api = axios.create({
  baseURL: "http://121.147.38.29:8000",
});

export const getProgressData = () => api.get("/data/progress/");
// export const getSimulateData = (data) => api.post("/simulate/", data);
export const getSimulateData = (data) => api.post("/simulate/", data);