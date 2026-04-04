import { useState, useRef } from "react";
import { analyzeResume } from "../services/api";
import ResultCard from "./ResultCard";
import Loader from "./Loader";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
 const fileInputRef = useRef();
  const handleUpload = async () => {
    if (!file) {
      alert("Upload resume first");
      return;
    }

    try {
      setLoading(true);
      const data = await analyzeResume(file);
      setResult(data);
    } catch (err) {
      alert("Error analyzing resume");
      print(err)
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Upload */}
      <div className="border-2 border-dashed p-6 text-center rounded-lg mb-4">
            <input
        type="file"
        ref={fileInputRef}
        onChange={(e) => setFile(e.target.files[0])}
      />
        {file && <p className="text-green-600 mt-2">{file.name}</p>}
      </div>
          <button
      onClick={() => {
        setFile(null);
        setResult(null);

        // 🔥 Clear input UI
        if (fileInputRef.current) {
          fileInputRef.current.value = "";
        }
      }}
      className="mt-2 w-full bg-gray-400 text-white p-2 rounded"
    >
      Clear
    </button>
     

      {/* Button */}
        <button
      onClick={handleUpload}
      disabled={!file || loading}
      className="w-full bg-blue-500 text-white p-3 rounded disabled:bg-gray-300"
    >
      Analyze Resume
    </button>

      {/* Loader */}
      {loading && <Loader />}

      {/* Result */}
      {result && <ResultCard result={result} />}
    </div>
  );
}

export default FileUpload;