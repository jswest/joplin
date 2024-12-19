export function getTags(raw) {
  if (!raw) {
    return [];
  }
  return raw
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean)
    .sort();
}
