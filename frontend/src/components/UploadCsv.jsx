import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  Card,
  Button,
  Form,
  CardBody,
  CardHeader,
  ProgressBar,
  Table,
} from "react-bootstrap";
import "./FileUpload.css";
import { BsArrowClockwise } from "react-icons/bs";
import apiCall from "../utils/fetch";

const FileUpload = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [fileList, setFileList] = useState([]);

  const { getRootProps, getInputProps } = useDropzone({
    accept: ".csv",
    onDrop: (acceptedFiles) => {
      setUploadedFiles(acceptedFiles);
    },
  });
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (uploadedFiles.length === 0) {
      console.log("No files selected");
      return;
    }

    const formData = new FormData();
    const file = uploadedFiles[0];
    formData.append("file", file);
    formData.append("filename", file.name);

    const token = localStorage.getItem("token");
    if (!token) {
      console.error("Token is missing");
      return;
    }

    const headers = {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    };

    try {
      const options = {
        method: "POST",
        headers: headers,
        body: formData,
      };
      const data = await apiCall("/api/csv/upload", options);
      if (data && data.data) {
        setFileList([data.data, ...fileList]);
        setUploadedFiles([]);
        setTimeout(() => refreshFileData(data.data._id), 1000);
      } else {
        console.error("Failed to upload file");
        alert("Failed to upload file");
      }
    } catch (error) {
      console.error("An error occurred during file upload", error);
      if (error.response.data.error) alert(error.response.data.error);
      else alert("An error occurred during file upload");
    }
  };
  const fetchProcessedList = async () => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    let data = await apiCall(`/api/csv/list/?page_size=100`, options);
    if (data.data) {
      data.data.map((file) => {
        if (file.status === "in_progress" || file.status === "pending")
          setTimeout(() => refreshFileData(file._id), 1000);
      });
      setFileList(data.data);
    }
  };
  useState(() => {
    fetchProcessedList();
  }, [fileList]);
  const refreshFileData = async (file_id) => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    let data = await apiCall(`/api/csv/get/${file_id}`, options);

    if (["in_progress", "pending"].includes(data.status)) {
      setTimeout(() => refreshFileData(file_id), 1000);
    }
    if (data) {
      setFileList((fileList) =>
        fileList.map((file) => {
          if (file._id === file_id) {
            return data;
          } else {
            return file;
          }
        })
      );
    }
  };
  return (
    <>
      <Card style={{ width: "40%", margin: "auto", marginTop: "5%" }}>
        <CardHeader style={{ textAlign: "center" }}>Upload CSV File</CardHeader>
        <CardBody>
          <Form onSubmit={handleSubmit} encType="multipart/form-data">
            <Form.Group>
              <div {...getRootProps()} className="dropzone text-center">
                <input
                  {...getInputProps()}
                  type="file"
                  accept=".csv"
                  multiple={false}
                />
                <h6>Drag and drop CSV files here, or click to browse.</h6>
              </div>
            </Form.Group>
            <p style={{ textAlign: "center", color: "blue" }}>
              {uploadedFiles?.[0]?.name}
            </p>
            <Button
              type="submit"
              className="mt-3"
              disabled={uploadedFiles.length === 0}
              variant="primary"
              style={{ width: "100%" }}
            >
              Upload
            </Button>
          </Form>
        </CardBody>
      </Card>

      <Card style={{ width: "100%", margin: "auto", marginTop: "5%" }}>
        <CardHeader>Uploaded Files</CardHeader>
        <Table striped bordered>
          <thead>
            <tr>
              <th>Filename</th>
              <th>State</th>
              <th>Progress</th>
              <th style={{ width: "5%", padding: "0" }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {fileList.map((file, index) => (
              <tr key={index}>
                <td>{file.filename}</td>
                <td>{file.status}</td>
                <td>
                  <ProgressBar
                    now={100}
                    label={
                      file.status === "failed"
                        ? file.error
                        : `${file.progress} rows processed`
                    }
                    variant={
                      file.status === "failed"
                        ? "danger"
                        : file.status === "processed"
                        ? "success"
                        : "warning"
                    }
                  />
                </td>
                <td>
                  <Button
                    variant="info"
                    size="sm"
                    className="btn btn-sm"
                    onClick={() => refreshFileData(file._id)}
                  >
                    <BsArrowClockwise />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Card>
    </>
  );
};

export default FileUpload;
