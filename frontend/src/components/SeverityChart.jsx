import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function SeverityChart({ data }) {
  return (
    <BarChart width={400} height={250} data={data}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="count" fill="#6366f1"/>
    </BarChart>
  );
}
