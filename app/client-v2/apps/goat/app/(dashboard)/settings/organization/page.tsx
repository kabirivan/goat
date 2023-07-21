import { makeStyles } from "@/lib/theme";

import { Tabs } from "@p4b/ui/components/Navigation/Tabs";

import ManageUsers from "./ManageUsers";
import Overview from "./Overview";
import Teams from "./Teams";

const Organization = () => {
  const { classes, cx } = useStyles();

  const tabs = [
    {
      child: <Overview />,
      name: "Overview",
    },
    {
      child: <ManageUsers />,
      name: "Manage users",
    },
    {
      child: <Teams />,
      name: "Teams",
    },
    {
      child: <div>overview</div>,
      name: "Settings",
    },
  ];

  return (
    <>
      <Tabs tabs={tabs} className={classes.tabs} />
    </>
  );
};

const useStyles = makeStyles({ name: { Organization } })((theme) => ({
  settingSection: {
    padding: theme.spacing(2),
  },
  tabs: {
    padding: "0",
  },
  bannerText: {
    color: "white",
  },
  extensionButtonWrapper: {
    marginBottom: theme.spacing(5),
  },
  button: {
    marginTop: theme.spacing(3),
    padding: `${theme.spacing(1)}px ${theme.spacing(2) + 2}px`,
    fontSize: "13px",
  },
}));

export default Organization;
