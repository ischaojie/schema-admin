import { useEffect, useState } from "react";
import { RJSFSchema } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import { Form as SchemaForm } from "@rjsf/mui";
import { Form, useLoaderData } from "react-router-dom";
import { getModel, saveModelData } from "../services/models";
import { Snackbar, Alert } from "@mui/material";

export async function loader({ params }) {
  const modelName = params.modelId;
  const model = await getModel(modelName);
  return { modelName, model };
}

export default function Model(props) {
  const { modelName, model } = useLoaderData();
  const [open, SetOpen] = useState(false);
  const [modelData, setModelData] = useState({});

  useEffect(() => {
    setModelData(model.data);
  }, [model.data]);

  const Submit = (e) => {
    saveModelData(modelName, e.formData);
    SetOpen(true);
    setModelData(e.formData);
  };

  const handleSnackBarClose = () => {
    SetOpen(false);
  };

  return (
    <div>
      <SchemaForm
        schema={model.schema}
        formData={modelData}
        validator={validator}
        onSubmit={Submit}
      />
      <div></div>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        open={open}
        autoHideDuration={6000}
        onClose={handleSnackBarClose}
        key={model.schema.title}
      >
        <Alert
          onClose={handleSnackBarClose}
          severity="success"
          sx={{ width: "100%" }}
        >
          {`Update ${model.schema.title} successfully!`}
        </Alert>
      </Snackbar>
    </div>
  );
}
