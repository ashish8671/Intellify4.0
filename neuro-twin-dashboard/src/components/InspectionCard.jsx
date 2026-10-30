import {
    FaBuilding,
    FaUserTie,
    FaCalendarAlt,
    FaMapMarkerAlt
} from "react-icons/fa";

function InspectionCard() {

    return (

        <div className="bg-slate-900 rounded-2xl border border-slate-700 p-5 mb-6">

            <h2 className="text-xl font-semibold text-white mb-5">

                Inspection Details

            </h2>

            <div className="grid grid-cols-4 gap-5">

                <Info
                    icon={<FaBuilding/>}
                    title="Building"
                    value="Bridge A-12"
                />

                <Info
                    icon={<FaCalendarAlt/>}
                    title="Inspection Date"
                    value="06 Aug 2026"
                />

                <Info
                    icon={<FaUserTie/>}
                    title="Inspector"
                    value="Ashish"
                />

                <Info
                    icon={<FaMapMarkerAlt/>}
                    title="Location"
                    value="Pune"
                />

            </div>

        </div>

    );

}

function Info({icon,title,value}){

    return(

        <div className="bg-slate-800 rounded-xl p-4">

            <div className="text-cyan-400 text-xl mb-2">

                {icon}

            </div>

            <p className="text-slate-400 text-sm">

                {title}

            </p>

            <h3 className="text-white font-semibold">

                {value}

            </h3>

        </div>

    )

}

export default InspectionCard;