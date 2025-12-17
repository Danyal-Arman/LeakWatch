export async function fetchPosts(page = 1, limit = 10) {
  const res = await fetch(
    `http://localhost:8000/posts?page=${page}&limit=${limit}`
  );
  return await res.json();
}
