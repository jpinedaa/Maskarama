import React, { useState, useRef, useEffect } from 'react';
import { ModalType } from '../../types/modal';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: ModalType;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, type }) => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [apiKey, setApiKey] = useState<string>("");
  const modalRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (isOpen) {
      modalRef.current?.showModal();
    } else {
      modalRef.current?.close();
    }
  }, [isOpen]);

  const handleSubmit = () => {
    switch (type) {
      case ModalType.LOGIN:
        console.log("Logging in with:", email, password);
        break;
      case ModalType.SIGNUP:
        console.log("Signing up with:", email, password);
        break;
      case ModalType.SETTINGS:
        console.log("Saving API key:", apiKey);
        break;
    }
    onClose();
  };

  const renderContent = () => {
    switch (type) {
      case ModalType.LOGIN:
        return (
          <>
            <h3 className="font-bold text-lg">Login</h3>
            <div className="form-control">
              <label className="label">
                <span className="label-text">Email</span>
              </label>
              <input 
                type="email" 
                placeholder="Enter your email" 
                className="input input-bordered" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="form-control mt-4">
              <label className="label">
                <span className="label-text">Password</span>
              </label>
              <input 
                type="password" 
                placeholder="Enter your password" 
                className="input input-bordered" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </>
        );
      case ModalType.SIGNUP:
        return (
          <>
            <h3 className="font-bold text-lg">Sign Up</h3>
            <div className="form-control">
              <label className="label">
                <span className="label-text">Email</span>
              </label>
              <input 
                type="email" 
                placeholder="Enter your email" 
                className="input input-bordered" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="form-control mt-4">
              <label className="label">
                <span className="label-text">Password</span>
              </label>
              <input 
                type="password" 
                placeholder="Create a password" 
                className="input input-bordered" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </>
        );
      case ModalType.SETTINGS:
        return (
          <>
            <h3 className="font-bold text-lg">Settings</h3>
            <div className="form-control">
              <label className="label">
                <span className="label-text">API Key</span>
              </label>
              <input 
                type="text" 
                placeholder="Enter API Key" 
                className="input input-bordered" 
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
            </div>
          </>
        );
    }
  };

  return (
    <dialog id="modal" className="modal max-h-screen" ref={modalRef}>
      <div className="modal-box">
        <form method="dialog">
          <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
        </form>
        {renderContent()}
        <div className="modal-action">
          <button className="btn" onClick={onClose}>Close</button>
          <button className="btn btn-primary" onClick={handleSubmit}>
            {type === ModalType.LOGIN ? 'Login' : type === ModalType.SIGNUP ? 'Sign Up' : 'Save'}
          </button>
        </div>
      </div>
    </dialog>
  );
};

export default Modal;