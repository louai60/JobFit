import React, { useState, useEffect } from "react";
import { toast } from "sonner";
import { uploadResume } from "../services/resumeService";
import { Upload, CheckCircle, AlertCircle, FileText } from "lucide-react";

const ResumeUploadForm = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "analyzing" | "success" | "error">("idle");
  const [progress, setProgress] = useState(0);
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [isSubmitDisabled, setIsSubmitDisabled] = useState(false);

  useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file);
      setFileUrl(url);
      return () => URL.revokeObjectURL(url);
    }
  }, [file]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files ? event.target.files[0] : null;
    setFile(selectedFile);
    setStatus("idle");
    setProgress(0); 
    setIsSubmitDisabled(false); 
  };

  const analyzeResume = async () => {
    setStatus("analyzing");
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((prev) => (prev < 90 ? prev + 10 : prev));
    }, 300);

    try {
      const formData = new FormData();
      if (file) formData.append("file", file);

      await uploadResume(formData);

      clearInterval(interval);
      setProgress(100);
      setStatus("success");
      toast.success("Resume uploaded and analyzed successfully!");
      setIsSubmitDisabled(true);
    } catch (error: any) {
      clearInterval(interval);
      setStatus("error");
      toast.error(error.message || "Failed to analyze resume.");
    } finally {
      setTimeout(() => {
        setProgress(0);
      }, 500);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      toast.error("Please select a file to upload.");
      return;
    }
    await analyzeResume();
  };

  return (
    <main className="min-h-screen w-full flex items-center justify-center bg-gray-50 p-4">
      <style>
        {`
          @keyframes scan {
            0% { top: -5%; opacity: 0.5; }
            50% { opacity: 0.8; }
            100% { top: 105%; opacity: 0.5; }
          }
        `}
      </style>

      <div className="w-full max-w-5xl bg-white rounded-lg shadow-lg p-6 space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900">Resume Upload</h1>
          <p className="mt-2 text-gray-600">Upload your resume for AI analysis</p>
        </div>

        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-6">
          {/* File Upload Section */}
          <div className="relative w-full">
            <input
              type="file"
              id="resume-upload"
              className="hidden"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              aria-label="Upload resume"
            />
            <label
              htmlFor="resume-upload"
              className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer
                ${status === "success" ? "border-green-400" : "border-gray-300"} 
                ${status === "error" ? "border-red-400" : "hover:bg-gray-50"}`}
            >
              {!file && (
                <div className="flex flex-col items-center">
                  <Upload className="w-12 h-12 text-gray-400" />
                  <p className="mt-2 text-sm text-gray-500">Click to upload or drag and drop</p>
                  <p className="text-xs text-gray-500">PDF, DOC, or DOCX (max 10MB)</p>
                </div>
              )}

              {file && (
                <div className="flex flex-col items-center">
                  <FileText className="w-12 h-12 text-gray-400" />
                  <p className="mt-2 text-sm text-gray-500">{file.name}</p>
                  <p className="text-xs text-gray-500">PDF, DOC, or DOCX (max 10MB)</p>
                </div>
              )}
            </label>
          </div>

          {/* File Preview Section */}
          <div className="relative h-64 border-2 border-gray-300 rounded-lg overflow-hidden">
            {file && file.type === "application/pdf" ? (
              <object
                data={fileUrl ?? ""}
                type="application/pdf"
                className="w-full h-full"
                aria-label="PDF preview"
              >
                <div className="h-full flex flex-col items-center justify-center">
                  <p className="text-sm font-medium text-gray-700">PDF preview not available</p>
                </div>
              </object>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400">
                <p className="text-sm">File preview will appear here</p>
              </div>
            )}

            {status === "analyzing" && (
              <div
                className="absolute inset-0 w-full bg-[#422afb]/40 backdrop-blur-md"
                style={{
                  animation: "scan 1.5s linear infinite",
                  background: "linear-gradient(transparent, #422afb, transparent)",
                }}
              />
            )}
          </div>

          <div className="col-span-2 flex justify-center">
            <button
              type="submit"
              className={`px-6 py-2 rounded-md text-white font-medium ${
                isSubmitDisabled || status === "analyzing"
                  ? "bg-[#422afb] cursor-not-allowed"
                  : "bg-[#422afb] hover:bg-[#2207f7]"
              }`}
              disabled={isSubmitDisabled || status === "analyzing"}
            >
              {status === "analyzing" ? "Analyzing..." : "Submit Resume"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
};

export default ResumeUploadForm;
