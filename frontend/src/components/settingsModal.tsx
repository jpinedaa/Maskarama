import React, { useState, useRef, useEffect } from 'react';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose }) => {
  const [apiKey, setApiKey] = useState<string>("");
  const modalRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (isOpen) {
      modalRef.current?.showModal();
    } else {
      modalRef.current?.close();
    }
  }, [isOpen]);

  const handleSave = () => {
    // Save the API key
    console.log("Saving API key:", apiKey);
    onClose();
  };

  return (
    <dialog id="settings_modal" className="modal max-h-screen" ref={modalRef}>
      <div className="modal-box">
        <form method="dialog">
          <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
        </form>
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
        <div className="modal-action">
          <button className="btn" onClick={onClose}>Close</button>
          <button className="btn btn-primary" onClick={handleSave}>Save</button>
        </div>
      </div>
    </dialog>
  );
};

export default SettingsModal;