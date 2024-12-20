export function getArrayField(raw) {
  if (!raw) {
    return [];
  }
  return raw
    .split(",")
    .map((d) => d.trim())
    .filter(Boolean)
    .sort();
}

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
