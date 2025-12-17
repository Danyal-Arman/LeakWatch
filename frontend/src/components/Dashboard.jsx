import { useEffect, useState } from "react";
import { fetchPosts } from "../api/postsApi";
import SeverityBadge from "./SeverityBadge";
import SeverityChart from "./SeverityChart";

export default function Dashboard() {
    const [severity, setSeverity] = useState("all");
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);


  const PAGE_SIZE = 10;

 useEffect(() => {
  fetchPosts(page, PAGE_SIZE).then(res => {
    setPosts(res.data);
    setTotalPages(res.pages);
  });
}, [page]);

  const filtered = severity === "all"
    ? posts
    : posts.filter(p => p.meta?.severity === severity);


  const severityData = ["high", "medium", "low"].map(level => ({
    name: level,
    count: posts.filter(p => p.meta?.severity === level).length
  }));

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">
        Social Media Monitoring for Data Leaks
      </h1>

      {/* Summary + Chart */}
      <div className="flex gap-6 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <p>Total Leaks</p>
          <h2 className="text-xl font-bold">{posts.length}</h2>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <SeverityChart data={severityData} />
        </div>
      </div>

      {/* Filter */}
      <select
        className="mb-4 p-2 border rounded"
        onChange={(e) => {
          setSeverity(e.target.value);
          setPage(1);
        }}
      >
        <option value="all">All Severities</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      {/* Table */}
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2">Platform</th>
              <th className="p-2">Organization</th>
              <th className="p-2">Description</th>
              <th className="p-2">Severity</th>
              <th className="p-2">Source</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(post => (
              <tr key={post.post_id} className="border-t">
                <td className="p-2">{post.platform}</td>
                <td className="p-2">{post.user}</td>
                <td className="p-2">{post.text.slice(0, 60)}...</td>
                <td className="p-2">
                  <SeverityBadge severity={post.meta?.severity} />
                </td>
                <td className="p-2">
                  {post.meta?.urls?.[0] ? (
                    <a href={post.meta.urls[0]} target="_blank" className="text-blue-600">
                      View
                    </a>
                  ) : "N/A"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 flex gap-2">
      <button
  disabled={page === 1}
  onClick={() => setPage(p => p - 1)}
>
  Prev
</button>

<button
  disabled={page === totalPages}
  onClick={() => setPage(p => p + 1)}
>
  Next
</button>

      </div>
    </div>
  );
}
