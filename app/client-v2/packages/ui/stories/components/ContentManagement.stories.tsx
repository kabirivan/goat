import type { Meta, StoryObj } from "@storybook/react/dist";

import ContentManagement from "../../components/temporary/contentManagement/ContentManagement";
import { ThemeProvider } from "../theme";

const meta: Meta<typeof ContentManagement> = {
  component: ContentManagement,
  tags: ["autodocs"],
  title: "Pages/Dashboard/ContentManagement",
  argTypes: {},
  decorators: [
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof ContentManagement>;

export const Warning: Story = {
  args: {},
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/tu6pPILBRSUuy3Hbu8Lphk/Goat-3.0?type=design&node-id=11533-159301&t=HR0djJcCsGmFmiKK-0",
    },
  },
};
