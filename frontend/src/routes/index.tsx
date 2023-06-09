import { useLoaderData } from "react-router-dom";
import { getMetadata } from "../services/schemas";

export async function loader() {
  const metadata = await getMetadata();
  return { metadata };
}

export default function Index() {
  const { metadata } = useLoaderData();

  return (
    <p id="zero-state">
      There are total <span className="text-red">{metadata.total}</span> models.
      <br />
    </p>
  );
}
