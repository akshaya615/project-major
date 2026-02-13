import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",  // Backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

export const predictSeverity = (data) =>
  API.post("/predict/predict-severity", data);

export const getHotspots = () =>
  API.get("/hotspots");

export const getAlerts = () =>
  API.get("/alerts");