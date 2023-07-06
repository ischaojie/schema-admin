import { useEffect, useState } from "react";
import { RJSFSchema } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import { Form as SchemaForm } from "@rjsf/mui";
import { Form, useLoaderData } from "react-router-dom";
import { getSchema, saveSchemaData } from "../services/schemas";
import { Snackbar, Alert } from "@mui/material";

export async function loader({ params }) {
  const schemaId = params.schemaId;
  const schema = await getSchema(schemaId);
  return { schemaId, schema };
}

export default function Schema(props) {
  const { SchemaName, schema } = useLoaderData();
  const [open, SetOpen] = useState(false);
  const [schemaData, setSchemaData] = useState({});

  useEffect(() => {
    setSchemaData(schema.data);
  }, [schema.data]);

  const Submit = (e) => {
    saveSchemaData(SchemaName, e.formData);
    SetOpen(true);
    setSchemaData(e.formData);
  };

  const handleSnackBarClose = () => {
    SetOpen(false);
  };

  return (
    <div>
      <SchemaForm
        schema={schema.struct}
        uiSchema={schema.ui}
        formData={schemaData}
        validator={validator}
        onSubmit={Submit}
      />
      <div></div>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        open={open}
        autoHideDuration={6000}
        onClose={handleSnackBarClose}
        key={schema.struct.title}
      >
        <Alert
          onClose={handleSnackBarClose}
          severity="success"
          sx={{ width: "100%" }}
        >
          {`Update ${schema.struct.title} successfully!`}
        </Alert>
      </Snackbar>
    </div>
  );
}
