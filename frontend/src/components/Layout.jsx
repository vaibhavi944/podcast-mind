import React from 'react';
import { NavLink } from 'react-router-dom';
import { Compass, Search, Heart, Sparkles } from 'lucide-react';
import { cn } from '../lib/utils';

const Layout = ({ children }) => {
  const navItems = [
    { to: "/", icon: Compass, label: "Discover" },
    { to: "/search", icon: Search, label: "Search" },
    { to: "/explore", icon: Sparkles, label: "Explore" },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar - Desktop */}
      <aside className="fixed left-0 top-0 hidden h-full w-64 border-r bg-card md:block">
        <div className="flex h-full flex-col p-6">
          <div className="flex items-center gap-2 mb-10 px-2">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold tracking-tight">PodcastMind</span>
          </div>

          <nav className="space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-primary text-primary-foreground" 
                    : "text-muted-foreground hover:bg-secondary hover:text-secondary-foreground"
                )}
              >
                <item.icon className="h-5 w-5" />
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="mt-auto">
            <div className="rounded-xl bg-primary/5 p-4 border border-primary/10">
              <p className="text-xs font-semibold text-primary uppercase tracking-wider mb-2">Zero Friction</p>
              <p className="text-xs text-muted-foreground leading-relaxed">
                No accounts. No trackers. Just semantic intelligence.
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="md:pl-64">
        {/* Mobile Header */}
        <header className="sticky top-0 z-30 flex h-16 items-center border-b bg-background/80 backdrop-blur-md px-6 md:hidden">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded bg-primary flex items-center justify-center">
              <Sparkles className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="font-bold tracking-tight">PodcastMind</span>
          </div>
        </header>

        <div className="p-6 md:p-10 max-w-7xl mx-auto">
          {children}
        </div>
      </main>

      {/* Mobile Nav - Bottom */}
      <nav className="fixed bottom-0 left-0 z-40 flex h-16 w-full items-center justify-around border-t bg-card px-6 md:hidden">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => cn(
              "flex flex-col items-center gap-1 text-[10px] font-medium transition-colors",
              isActive ? "text-primary" : "text-muted-foreground"
            )}
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Layout;
