

const FarmerList = ({ farmers }) => {
  return (
    <div>
        <h2 className="text-2xl font-bold mb-4 text-green-700">Registered Farmers</h2>
        <div className="space-y-4">
        <table className="w-full bg-white border border-gray-300 rounded-lg shadow-md">
          <thead>
            <tr>
              <th className="border border-gray-300 px-4 py-2 text-left text-gray-700 text-sm">Name</th>
              <th className="border border-gray-300 px-4 py-2 text-left text-gray-700 text-sm">Phone</th>
              <th className="border border-gray-300 px-4 py-2 text-left text-gray-700 text-sm">Location</th>
              <th className="border border-gray-300 px-4 py-2 text-left text-gray-700 text-sm">Farm Size</th>
            </tr>
          </thead>
          <tbody>
            {farmers.map((farmer, index) => (
              <tr key={index}>
                <td className="border border-gray-300 px-4 py-2 text-sm">{farmer.name}</td>
                <td className="border border-gray-300 px-4 py-2 text-sm">{farmer.phone}</td>
                <td className="border border-gray-300 px-4 py-2 text-sm">{farmer.location}</td>
                <td className="border border-gray-300 px-4 py-2 text-sm">{farmer.farmSize}</td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
    </div>
  );
};

export default FarmerList;