import React, { useState, useEffect } from 'react';
import Modal from './modal';
import ProgressBar from '../progressBar';
import { ModalType } from '../../types/modal';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [modalType, setModalType] = useState<ModalType>(ModalType.LOGIN);
  const totalPhases = 4;

 

  const openModal = (type: ModalType) => {
    setModalType(type);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const renderNavItems = () => (
    <React.Fragment>
      
      {isLoggedIn ? (
        <li><a onClick={() => setIsLoggedIn(false)}>Logout</a></li>
      ) : (
        <div className='flex flex-col md:flex-row'>
          <li className='text-yellow-400 text-lg'><a onClick={() => openModal(ModalType.SIGNUP)}>Sign Up</a></li>
          <li className='text-yellow-400 text-lg'><a onClick={() => openModal(ModalType.LOGIN)}>Log In</a></li>
        </div>
      )}

      <li className='text-yellow-400 text-lg place-self-end'><a onClick={() => openModal(ModalType.SETTINGS)}>Settings</a></li>
    </React.Fragment>
  );

  return (
    <div className="drawer h-[100vh] max-h-[100vh] overflow-hidden">
      <input id="my-drawer-3" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex flex-row">
        {/* Main content area */}
        <div className="flex flex-col flex-grow">
          {/* Navbar */}
          <div className="hidden navbar bg-primary w-full z-50 shadow-lg">
            <div className="flex-none lg:hidden">
              <label htmlFor="my-drawer-3" aria-label="open sidebar" className="btn btn-square btn-ghost">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block w-6 h-6 stroke-yellow-400">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </label>
            </div>
            <div className="flex-1 px-2 mx-2 text-yellow-400 text-xl">Echoes of Creation</div>
            <div className="flex-none hidden lg:block">
              <ul className="menu menu-horizontal py-0 px-8">
                {renderNavItems()}
              </ul>
            </div>
          </div>

          {/* Page content here */}
          <main className="flex-grow">
            {children}
          </main>
        </div>

        
      </div> 
      
      <div className="drawer-side z-50">
        <label htmlFor="my-drawer-3" aria-label="close sidebar" className="drawer-overlay"></label> 
        <ul className="menu p-4 w-80 min-h-full bg-primary justify-between">
          {renderNavItems()}
        </ul>
      </div>

      <Modal 
        isOpen={isModalOpen}
        onClose={closeModal}
        type={modalType}
      />
    </div>
  );
};

export default Layout;