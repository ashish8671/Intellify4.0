function StatCard({
  title,
  value,
  icon,
  color,
  bg,
}) {
  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-700 shadow-lg p-5 hover:shadow-cyan-500/10 transition-all duration-300">

      <div className="flex justify-between items-center">

        <div>

          <p className="text-slate-400 text-sm">
            {title}
          </p>

          <h2 className={`text-4xl font-bold mt-3 ${color}`}>
            {value}
          </h2>

        </div>

        <div
          className={`${bg} ${color} p-4 rounded-xl text-2xl`}
        >
          {icon}
        </div>

      </div>

    </div>
  );
}

export default StatCard;