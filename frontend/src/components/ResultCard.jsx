function ResultCard({ result }) {
  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">Result</h2>

      {/* Score */}
      <div className="mb-4">
        <p className="font-semibold">Score: {result.score}%</p>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-green-500 h-4 rounded-full"
            style={{ width: `${result.score}%` }}
          ></div>
        </div>
      </div>

      {/* Sections */}
      <div className="bg-gray-50 p-4 rounded mb-2">
        <h3 className="font-semibold">Strengths</h3>
        <p>{result.strengths}</p>
      </div>

      <div className="bg-gray-50 p-4 rounded mb-2">
        <h3 className="font-semibold">Weakness</h3>
        <p>{result.weakness}</p>
      </div>

      <div className="bg-gray-50 p-4 rounded">
        <h3 className="font-semibold">Suggestions</h3>
        <p>{result.suggestions}</p>
      </div>
    </div>
  );
}

export default ResultCard;