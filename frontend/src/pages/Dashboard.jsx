import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { getResumes } from "../services/api";

function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await getResumes();
      setData(res);
    } catch (err) {
      console.log("Unauthorized or error");
    }
  };

  return (
    <MainLayout>
      <h1 className="text-2xl font-bold mb-6">📊 Dashboard</h1>

      {data.length === 0 ? (
        <p>No resumes found</p>
      ) : (
        <div className="space-y-4">
          {data.map((item) => (
            <div
              key={item.id}
              className="bg-white p-5 rounded-xl shadow-md"
            >
              {/* Filename */}
              <h2 className="text-lg font-bold mb-2">
                📄 {item.filename}
              </h2>

              {/* Score */}
              <div className="mb-3">
                <p
                  className={`font-bold ${
                    item.score >= 75
                      ? "text-green-600"
                      : item.score >= 50
                      ? "text-yellow-500"
                      : "text-red-500"
                  }`}
                >
                  Score: {item.score}%
                </p>

                {/* Progress Bar */}
                <div className="w-full bg-gray-200 rounded h-2 mt-1">
                  <div
                    className="h-2 rounded bg-blue-500"
                    style={{ width: `${item.score}%` }}
                  ></div>
                </div>
              </div>

              {/* Strengths */}
              <div className="mb-2">
                <p className="font-semibold text-green-600">💪 Strengths</p>
                <p className="text-gray-700">{item.strengths}</p>
              </div>

              {/* Weakness */}
              <div className="mb-2">
                <p className="font-semibold text-red-500">⚠️ Weakness</p>
                <p className="text-gray-700">{item.weakness}</p>
              </div>

              {/* Suggestions */}
              <div>
                <p className="font-semibold text-blue-600">💡 Suggestions</p>
                <p className="text-gray-700">{item.suggestions}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </MainLayout>
  );
}

export default Dashboard;