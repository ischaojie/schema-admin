

// /api/models/<name>
export async function getModel(name: string) {
  return await fetch(`/conger/api/models/${name}`, {
    method: "GET",
  })
    .then((rsp) => rsp.json())
    .catch((err) => console.error(err));
}

// /api
export async function getMetadata() {
  return await fetch("/conger/api", { method: "GET" })
    .then((rsp) => rsp.json())
    .catch((err) => console.error(err));
}

export async function saveModelData(name: string, data: any) {
  return await fetch(`/conger/api/models/${name}/data`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((rsp) => rsp.json())
    .catch((err) => console.error(err));
}
