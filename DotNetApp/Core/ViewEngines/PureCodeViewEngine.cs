using System;
using System.Web.Mvc;

namespace DotNetApp.Core.ViewEngines
{
    public class PureCodeViewEngine : IViewEngine
    {
        public ViewEngineResult FindPartialView(ControllerContext controllerContext, string partialViewName, bool useCache)
        {
            return FindView(controllerContext, partialViewName, "", false);
        }

        public ViewEngineResult FindView(ControllerContext controllerContext, string viewName, string masterName, bool useCache)
        {
            var found = FindView(controllerContext, viewName);
            if(found.Item1 == null)
            {
                return new ViewEngineResult(found.Item2);
            }

            return new ViewEngineResult(found.Item1, this);
        }

        public void ReleaseView(ControllerContext controllerContext, IView view)
        {
            // TODO: Release the view
        }

        protected virtual Tuple<IView, string[]> FindView(ControllerContext controllerContext, string viewName)
        {
            var prefixViewName = viewName.StartsWith(ViewEnginePrefix, StringComparison.OrdinalIgnoreCase) ? viewName : ViewEnginePrefix + viewName;

            var found = new PureCodeView(viewName);
            var searchedLocations = new string[] { };

            return new Tuple<IView, string[]>(found, searchedLocations);
        }

        public string ViewEnginePrefix { get; set; } = "vicon";
    }
}
