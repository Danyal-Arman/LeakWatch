import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer } from "recharts";

export default function SeverityChart({ data }) {

  const barColor = {
  high: "#ef4444",   // medium red
  medium: "#facc15", // medium yellow
  low: "#22c55e"     // medium green
};

  return (
    <div className="w-full h-[280px]">
      <ResponsiveContainer>
        <BarChart data={data}>

          <XAxis
            dataKey="name"
            tickFormatter={(v) => v.charAt(0).toUpperCase() + v.slice(1)}
            tick={{ fill: "#9ca3af" }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            tick={{ fill: "#9ca3af" }}
            axisLine={false}
            tickLine={false}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "#18181b",
              border: "none",
              borderRadius: "8px",
              color: "#fff"
            }}
            labelStyle={{ color: "#fff" }}
            itemStyle={{ color: "#fff" }}
          />

          <Bar
            dataKey="count"
            radius={[8, 8, 0, 0]}
            animationDuration={800}
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={barColor[entry.name]} />
            ))}
          </Bar>

        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}