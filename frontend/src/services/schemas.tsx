

// /api/models/<name>
export async function getSchema(name: string) {
  return await fetch(`/admin/api/schemas/${name}`, {
    method: "GET",
  })
    .then((rsp) => rsp.json())
    .catch((err) => console.error(err));
}

// /api
export async function getMetadata() {
  return await fetch("/admin/api", { method: "GET" })
    .then((rsp) => rsp.json())
    .catch((err) => console.error(err));
}

export async function saveSchemaData(name: string, data: any) {
  return await fetch(`/admin/api/schemas/${name}/data`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((rsp) => rsp.json())
    .catch((err) => console.error(err));
}
