import React from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';

// This component expects children in the format:
// <CodeBlockTabs groupId="my-code-example">
//   <TabItem value="python" label="Python">
//     <CodeBlock language="python">
//       {/* Python code here */}
//     </CodeBlock>
//   </TabItem>
//   <TabItem value="cpp" label="C++">
//     <CodeBlock language="cpp">
//       {/* C++ code here */}
//     </CodeBlock>
//   </TabItem>
// </CodeBlockTabs>

export default function CodeBlockTabs({ children, ...props }) {
  return (
    <Tabs {...props}>
      {/* Assuming children are already TabItem components */}
      {children}
    </Tabs>
  );
}
