function Loader() {
  return (
    <div className="fixed inset-0 bg-blue-500 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <p className="text-lg font-semibold">Analyzing Resume...</p>
      </div>
    </div>
  );
}

export default Loader;