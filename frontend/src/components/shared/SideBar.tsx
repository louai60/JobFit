import React, { useState } from "react";
import {
  Search,
  Home,
  LayoutDashboard,
  Users,
  Settings,
  HelpCircle,
  ChevronDown,
  ChevronRight,
  Folder,
  Mail,
  Calendar,
  Bell,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isResourcesOpen, setIsResourcesOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <div
      className={cn(
        "flex h-screen transition-all duration-300",
        isCollapsed ? "bg-gray-100" : "bg-white"
      )}
    >
      <aside
        className={cn(
          "flex flex-col bg-background border-r transition-all duration-300",
          isCollapsed ? "w-20" : "w-64"
        )}
      >
        <div className="flex items-center justify-between p-6 border-b">
          {!isCollapsed && (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-[#422afb] rounded-lg" />
              <span className="font-semibold">Dashboard</span>
            </div>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(!isCollapsed)}
            aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {isCollapsed ? <ChevronRight size={20} /> : <ChevronDown size={20} />}
          </Button>
        </div>

        {!isCollapsed && (
          <div className="px-4 py-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                type="search"
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 focus-visible:ring-emerald-700"
              />
            </div>
          </div>
        )}

        <nav className="flex-1 overflow-y-auto">
          <ul className="p-2 space-y-1">
            {[
              { icon: Home, label: "Home" },
              { icon: LayoutDashboard, label: "Dashboard" },
              { icon: Calendar, label: "Calendar" },
              { icon: Mail, label: "Messages" },
            ].map((item, index) => (
              <li key={index}>
                <Button variant="ghost" className="w-full justify-start">
                  <item.icon className="h-5 w-5 mr-3" />
                  {!isCollapsed && <span>{item.label}</span>}
                </Button>
              </li>
            ))}
            <li>
              <Button
                variant="ghost"
                className="w-full justify-start"
                onClick={() => setIsResourcesOpen(!isResourcesOpen)}
              >
                <div className="flex items-center">
                  <Folder className="h-5 w-5 mr-3" />
                  {!isCollapsed && <span>Resources</span>}
                </div>
                {!isCollapsed && (
                  <ChevronDown
                    className={cn(
                      "h-4 w-4 ml-auto transition-transform",
                      isResourcesOpen && "rotate-180"
                    )}
                  />
                )}
              </Button>
              {!isCollapsed && isResourcesOpen && (
                <ul className="mt-1 ml-4 space-y-1">
                  {[
                    { icon: Users, label: "Team" },
                    { icon: Bell, label: "Notifications" },
                  ].map((subItem, subIndex) => (
                    <li key={subIndex}>
                      <Button variant="ghost" className="w-full justify-start">
                        <subItem.icon className="h-5 w-5 mr-3" />
                        <span>{subItem.label}</span>
                      </Button>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          </ul>
        </nav>

        <div className="border-t">
          <ul className="p-2 space-y-1">
            {[
              { icon: Settings, label: "Settings" },
              { icon: HelpCircle, label: "Help" },
            ].map((item, index) => (
              <li key={index}>
                <Button variant="ghost" className="w-full justify-start">
                  <item.icon className="h-5 w-5 mr-3" />
                  {!isCollapsed && <span>{item.label}</span>}
                </Button>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      <main className="flex-1">
        {/* Your main content */}
      </main>
    </div>
  );
}
