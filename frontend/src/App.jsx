import {
  BrowserRouter,
  Link,
  Route,
  Routes,
  useLocation,
} from "react-router-dom"

import Dashboard from "./pages/Dashboard"
import Emails from "./pages/Emails"
import EmailDetails from "./pages/EmailDetails"
import Actions from "./pages/Actions"
import Settings from "./pages/Settings"

function Layout() {
  const location = useLocation()

  const navigation = [
    {
      name: "Dashboard",
      path: "/",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      ),
    },
    {
      name: "Emails",
      path: "/emails",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      name: "Actions",
      path: "/actions",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    {
      name: "Settings",
      path: "/settings",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
    },
  ]

  const activeNav = navigation.find((n) => location.pathname === n.path) || navigation[0]

  return (
    <div className="min-h-screen bg-slate-50/50 font-sans text-slate-800 antialiased flex flex-col">
      {/* Top Navbar */}
      <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-md shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between gap-4">
            {/* Left: Brand Logo & Title */}
            <Link to="/" className="flex items-center gap-3 group">
              <img
                src="/robot.png"
                alt="Maily Mascot"
                className="h-9 w-9 object-contain drop-shadow-xs group-hover:scale-105 transition-transform"
              />
              <div>
                <h1 className="text-lg font-bold tracking-tight text-slate-900 leading-tight">
                  Maily
                </h1>
                <p className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider">
                  AI Agent
                </p>
              </div>
            </Link>

            {/* Center: Horizontal Navigation Bar */}
            <nav className="flex items-center gap-1 sm:gap-2">
              {navigation.map((item) => {
                const active = location.pathname === item.path

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-sm font-semibold transition-all duration-200 ${
                      active
                        ? "bg-indigo-50 text-indigo-700 shadow-2xs border border-indigo-100"
                        : "text-slate-600 hover:bg-slate-100/80 hover:text-slate-900"
                    }`}
                  >
                    <span className={active ? "text-indigo-600" : "text-slate-400"}>
                      {item.icon}
                    </span>
                    <span className="hidden sm:inline">{item.name}</span>
                  </Link>
                )
              })}
            </nav>

            {/* Right: Status Badges & Profile */}
            <div className="flex items-center gap-3">
              <div className="hidden lg:flex items-center gap-2 bg-emerald-50 border border-emerald-200 rounded-full px-3 py-1">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-xs font-semibold text-emerald-800">Gmail Connected</span>
              </div>

              <div className="flex items-center gap-2 bg-indigo-50/80 border border-indigo-100/80 rounded-full px-3 py-1 shadow-2xs">
                <img src="/robot.png" alt="Robot AI" className="h-5 w-5 object-contain" />
                <span className="text-xs font-semibold text-indigo-700 hidden md:inline">Robot AI Online</span>
              </div>

              <div className="h-8 w-8 rounded-full bg-indigo-600 font-bold text-xs flex items-center justify-center text-white shadow-md shadow-indigo-100">
                P
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 p-4 sm:p-6 md:p-8 max-w-7xl w-full mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/emails" element={<Emails />} />
          <Route path="/emails/:id" element={<EmailDetails />} />
          <Route path="/actions" element={<Actions />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}

export default App