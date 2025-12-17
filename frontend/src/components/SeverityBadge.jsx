export default function SeverityBadge({ severity }) {
  const colors = {
    high: "red",
    medium: "orange",
    low: "green"
  };

  return (
    <span
      style={{
        padding: "4px 10px",
        borderRadius: "12px",
        color: "white",
        backgroundColor: colors[severity] || "gray",
        fontSize: "12px"
      }}
    >
      {severity.toUpperCase()}
    </span>
  );
}
