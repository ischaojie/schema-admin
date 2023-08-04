import axios from "axios";

// /api/models/<name>
export async function getSchema(name: string) {
  return await axios
    .get(`/admin/api/schemas/${name}`)
    .then((rsp) => rsp.data)
    .catch((err) => console.error(err));
}

// /api
export async function getMetadata() {
  return await axios
    .get("/admin/api")
    .then((rsp) => rsp.data)
    .catch((err) => console.error(err));
}

export async function saveSchemaData(name: string, data: any) {
  return await axios
    .post(`/admin/api/schemas/${name}/data`, data)
    .then((rsp) => rsp.data)
    .catch((err) => console.error(err));
}
