import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const fetchSecurityReports = async (page, limit) => {
  const { data } = await API.get(
    `/security/reports?page=${page}&limit=${limit}`
  );

  return data;
};