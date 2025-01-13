import React from "react";
import {
  DropdownMenu,
  DropdownMenuItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { FiAlignJustify } from "react-icons/fi";
import { Link, useNavigate } from "react-router-dom";
import { BsArrowBarUp } from "react-icons/bs";
import { FiSearch } from "react-icons/fi";
import { RiMoonFill, RiSunFill } from "react-icons/ri";
import { IoMdNotificationsOutline } from "react-icons/io";
import authService from "../../services/authService"; 

interface NavbarProps {
  onOpenSidenav: () => void;
  brandText: string;
  secondary?: boolean;
  avatar: string;
  userName?: string;
}

const Navbar: React.FC<NavbarProps> = ({
  onOpenSidenav,
  brandText,
  avatar,
  userName = "User",
}) => {
  const [darkmode, setDarkmode] = React.useState(false);
  const navigate = useNavigate(); // For redirecting to login page after logout

  // Handle Logout
  const handleLogout = () => {
    authService.logout(); // Call the logout function to clear cookies
    navigate("/login"); // Redirect to the login page
  };

  return (
    <nav className="sticky top-4 z-40 flex flex-row flex-wrap items-center justify-between rounded-xl bg-white/10 p-2 backdrop-blur-xl dark:bg-[#0b14374d]">
      <div className="ml-[6px]">
        <div className="flex items-center gap-1 text-sm">
          <Link to="/pages" className="text-gray-600 dark:text-gray-400">
            Pages
          </Link>
          <span className="text-gray-600 dark:text-gray-400">/</span>
          <span className="font-medium text-navy-700 dark:text-white">
            {brandText}
          </span>
        </div>
      </div>

      <div className="ml-auto flex items-center gap-4 rounded-full bg-white px-4 py-2 shadow-xl dark:bg-navy-800">
        <div className="flex items-center gap-2 rounded-full bg-gray-50 px-3 py-2 dark:bg-navy-900">
          <FiSearch className="h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search..."
            className="bg-transparent text-sm outline-none placeholder:text-gray-400 dark:text-white"
          />
        </div>

        <button onClick={onOpenSidenav} className="lg:hidden">
          <FiAlignJustify className="h-5 w-5 text-gray-600 dark:text-white" />
        </button>

        <DropdownMenu>
          <DropdownMenuTrigger className="flex items-center">
            <IoMdNotificationsOutline className="h-5 w-5 text-gray-600 dark:text-white" />
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-[360px] flex flex-col gap-3 rounded-[20px] bg-white p-4 shadow-xl dark:bg-navy-700 dark:text-white sm:w-[460px]"
            align="end"
          >
            <div className="flex items-center justify-between">
              <p className="text-base font-bold text-navy-700 dark:text-white">
                Notification
              </p>
              <button className="text-sm font-bold text-navy-700 dark:text-white">
                Mark all read
              </button>
            </div>
            <DropdownMenuItem asChild>
              <button className="flex w-full items-center">
                <div className="flex h-full w-[85px] items-center justify-center rounded-xl bg-gradient-to-b from-brandLinear to-brand-500 py-4 text-2xl text-white">
                  <BsArrowBarUp />
                </div>
                <div className="ml-2 flex h-full w-full flex-col justify-center rounded-lg px-1 text-sm">
                  <p className="mb-1 text-left text-base font-bold text-gray-900 dark:text-white">
                    New Update: Horizon UI Dashboard PRO
                  </p>
                  <p className="font-base text-left text-xs text-gray-900 dark:text-white">
                    A new update for your downloaded item is available!
                  </p>
                </div>
              </button>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <button
          onClick={() => {
            setDarkmode(!darkmode);
            document.body.classList.toggle("dark");
          }}
          className="flex items-center"
        >
          {darkmode ? (
            <RiSunFill className="h-5 w-5 text-gray-600 dark:text-white" />
          ) : (
            <RiMoonFill className="h-5 w-5 text-gray-600 dark:text-white" />
          )}
        </button>

        <DropdownMenu>
          <DropdownMenuTrigger className="flex items-center">
            <img
              src={avatar}
              alt="Profile"
              className="h-10 w-10 rounded-full object-cover"
            />
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="flex h-48 w-56 flex-col justify-start rounded-[20px] bg-white shadow-xl dark:!bg-navy-700 dark:text-white"
            align="end"
          >
            <div className="mt-3 ml-4">
              <div className="flex items-center gap-2">
                <p className="text-sm font-bold text-navy-700 dark:text-white">
                  👋 Hey, {userName}
                </p>
              </div>
            </div>
            <div className="mt-3 h-px w-full bg-gray-200 dark:bg-white/20" />
            <div className="mt-3 ml-4 flex flex-col">
              <a
                href="#profile"
                className="text-sm text-gray-800 dark:text-white hover:dark:text-white"
              >
                Profile Settings
              </a>
              <a
                href="#newsletter"
                className="mt-3 text-sm text-gray-800 dark:text-white hover:dark:text-white"
              >
                Newsletter Settings
              </a>
              <a
                href="#logout"
                onClick={handleLogout} // Trigger logout function
                className="mt-3 text-sm font-medium text-red-500 hover:text-red-500"
              >
                Log Out
              </a>
            </div>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </nav>
  );
};

export default Navbar;
