using DotNetApp.Core.ViewEngines;
using System.Web.Mvc;
using System.Web.Optimization;
using System.Web.Routing;

namespace DotNetApp
{
    public class MvcApplication : System.Web.HttpApplication
    {
        protected void Application_Start()
        {
            AreaRegistration.RegisterAllAreas();
            FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
            RouteConfig.RegisterRoutes(RouteTable.Routes);
            BundleConfig.RegisterBundles(BundleTable.Bundles);
            RegisterViewEngines(ViewEngines.Engines);
        }

        private void RegisterViewEngines(ViewEngineCollection engines)
        {
            engines.Insert(0, new PureCodeViewEngine());
        }
    }
}
