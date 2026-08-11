import React from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const Auth = () => {

    const [showPassword, setShowPassword] = React.useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
         const formData = new FormData(e.target);
         const data = Object.fromEntries(formData.entries());
         console.log(data);

    }
    return(
        <div className="flex items-center justify-center bg-white min-h-screen mx-auto">
            <div className="container max-w-md w-full mx-auto px-6 py-6">
                <div className="flex flex-col flex-row rounded-xl shadow-xl overflow-hidden">
                    {/* Left Side */}
                    <div className="w-full p-12">
                    <div className="flex flex-col">
                        <h3 className="text-3xl text-green-700 mb-2 font-bold">Welcome Back</h3>
                        <p className="text-gray-600">Login to your account</p>
                    </div>
                    {/* line */}
                     {/* <div className= "flex items-center mt-3">
                        <div className= "flex-grow border-t border-gray-300">
                            <span className="text-gray-700"></span>
                            <div className="flex-grow border-t border-gray-300"></div>
                        </div>
                    </div>
                     */}
                    {/* Authentication Form  */}
                    <form onSubmit={handleSubmit}>
                        {/* Email field */}
                        <div className="mb-4 mt-6">
                            <label htmlFor="email" className="block text-gray-700 font-semibold mb-2">Email address</label>
                            <input type="email" id="email" name="email" placeholder="Enter your email" className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                        </div>
                              {/* Password field */}
                         <div className="mb-4 mt-6">
                            <label htmlFor="password" className="block text-gray-700 font-semibold mb-2">Password</label>
                            <div className="relative">
                            <input type={showPassword ? "text" : "password"} id="password" name="password" placeholder="Enter your password" className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
                             <button type ="button" onClick={()=>setShowPassword(!showPassword)} className="absolute top-3 right-3 text-gray-500 hover:text-gray-700 focus:outline-none cursor-pointer">
                                {showPassword ? <FaEyeSlash /> : <FaEye />}
                                </button> 
                            </div>
                        </div>
                        {/* Remember checkbox */}
                        <div className="flex items-center justify-between mb-4 mt-6">
                           <div className="flex items-center gap-2">
                                <input type="checkbox" className="form-checkbox h-4 w-4 text-green-500" />
                                <span className="ml-2 text-gray-700 font-semibold">Remember me</span>
                            </div> 
                            <a href="#" className="text-amber-600 text-sm font-semibold hover:underline">Forgot Password</a>
                        </div>
                        {/*Login button */}
                        <div className="mt-6 mb-2">
                            <button className="w-full bg-green-700 text-white font-bold rounded cursor-pointer py-2 hover:bg-green-800">Login</button>
                        </div>
                    </form>
                </div>
                </div>

            </div>
        </div>
    )
}

export default Auth;