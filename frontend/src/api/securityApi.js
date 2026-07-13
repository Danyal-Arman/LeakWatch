import axios from "axios";

const API = axios.create({
  baseURL: "https://leakwatch.onrender.com",
});

export const fetchSecurityReports = async (page, limit) => {
  const { data } = await API.get(
    `/security/reports?page=${page}&limit=${limit}`
  );

  return data;
};