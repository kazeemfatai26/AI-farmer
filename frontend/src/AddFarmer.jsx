import {useState} from 'react';

const AddFarmer = ({ onAddFarmer }) => {
    const [fullName, setFullName] = useState('');
    const [gender, setGender] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [dob, setDob] = useState('');
    const [farmLocation, setFarmLocation] = useState('');
    const [farmSize, setFarmSize] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const newFarmer = { name: fullName, gender: gender, phone: phoneNumber, dob: dob, location: farmLocation, farmSize: farmSize };
        onAddFarmer(newFarmer);
    };

    return (
       <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4 text-green-700">Add Farmer</h2>
            <form onSubmit={handleSubmit} className="space-y-4">                      
            <div className="mb-4">
                    <label htmlFor="fullName" className="block text-gray-700 font-semibold mb-2">Full Name</label>
                    <input type="text" id="fullName" value={fullName} onChange={(e) => setFullName(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                </div>
               <div className="mb-4">
                    <label htmlFor="gender" className="block text-gray-700 font-semibold mb-2">Gender</label>
                    <select id="gender" value={gender} onChange={(e) => setGender(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required>
                        <option value="">Select Gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>

                <div className="mb-4">
                    <label htmlFor="phoneNumber" className="block text-gray-700 font-semibold mb-2">Phone Number</label>
                    <input type="tel" id="phoneNumber" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                </div>

                <div className="mb-4">
                    <label htmlFor="dob" className="block text-gray-700 font-semibold mb-2">Date of Birth</label>
                    <input type="date" id="dob" value={dob} onChange={(e) => setDob(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                </div>

                <div className="mb-4">
                    <label htmlFor="farmLocation" className="block text-gray-700 font-semibold mb-2">Farm Location</label>
                    <input type="text" id="farmLocation" value={farmLocation} onChange={(e) => setFarmLocation(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                </div>

                <div className="mb-4">
                    <label htmlFor="farmSize" className="block text-gray-700 font-semibold mb-2">Farm Size (acres)</label>
                    <input type="number" id="farmSize" value={farmSize} onChange={(e) => setFarmSize(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                </div>

                <button type="submit" className="w-full bg-green-700 text-white font-bold rounded cursor-pointer py-2 hover:bg-green-800">
                    Register Farmer
                </button>
                </form>
                </div>
    )
};

export default AddFarmer;