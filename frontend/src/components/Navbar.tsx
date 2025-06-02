import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white';
  };

  return (
    <nav className="bg-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-white text-xl font-bold">Buuks</span>
            </div>
            <div className="ml-10 flex items-baseline space-x-4">
              <Link
                to="/"
                className={`${isActive('/')} rounded-md px-3 py-2 text-sm font-medium`}
              >
                Dashboard
              </Link>
              <Link
                to="/configuration"
                className={`${isActive('/configuration')} rounded-md px-3 py-2 text-sm font-medium`}
              >
                Configuration
              </Link>
              <Link
                to="/database"
                className={`${isActive('/database')} rounded-md px-3 py-2 text-sm font-medium`}
              >
                Database
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;