import { useState, useEffect } from "react";

const FarmerList = () => {
  const [farmers, setFarmers] = useState([]);

  useEffect(() => {
    const loadFarmers = async () => {
      try {
        const response = await fetch("https://ai-farmer-56eq.onrender.com/fetchFarmers");
        const data = await response.json();
        setFarmers(data);
      } catch (error) {
        console.error("Error fetching farmers:", error);
      }
    };

    loadFarmers();
  }, []);
  return (
    <div>
        <h2 className="text-2xl font-bold mb-4 text-green-700">Registered Farmers</h2>
        <div className="space-y-4">
        <table className="w-full border border-gray-200 rounded-lg overflow-hidden">
        <thead className="bg-gray-100">
      <tr>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">S/N</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">Name</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">Phone</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">District</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">Sector</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">Crop</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">Planting Date</th>
      <th className="text-left px-4 py-2 text-sm font-semibold text-gray-700">Language</th>
    </tr>
  </thead>
  <tbody>
  {farmers.map((farmer, index) => (
    <tr key={farmer._id} className="border-t border-gray-200">
      <td className="px-4 py-2 text-sm text-gray-800">{index + 1}</td>
      <td className="px-4 py-2 text-sm text-gray-800">{farmer.name}</td>
      <td className="px-4 py-2 text-sm text-gray-800">{farmer.phone_number}</td>
      <td className="px-4 py-2 text-sm text-gray-800">{farmer.district}</td>
      <td className="px-4 py-2 text-sm text-gray-800">{farmer.sector}</td>
      <td className="px-4 py-2 text-sm text-gray-800">{farmer.crop_type}</td>
      <td className="px-4 py-2 text-sm text-gray-800">
        {new Date(farmer.planting_date).toLocaleDateString()}
      </td>
      <td className="px-4 py-2 text-sm text-gray-800">
        {farmer.preferred_language === "rw" ? "Kinyarwanda" : "English"}
      </td>
    </tr>
  ))}
</tbody>
</table>
        </div>
    </div>
  );
};

export default FarmerList;