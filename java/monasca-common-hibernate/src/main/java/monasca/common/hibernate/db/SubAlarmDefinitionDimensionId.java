/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Embeddable;

@Embeddable
public class SubAlarmDefinitionDimensionId implements Serializable {

  @Column(name = "sub_alarm_definition_id", length = 36, nullable = false)
  private String sub_alarm_definition_id;

  @Column(name = "dimension_name", length = 50, nullable = false)
  private String dimension_name;

  public SubAlarmDefinitionDimensionId() {
    this("", "");
  }

  public SubAlarmDefinitionDimensionId(String sub_alarm_definition_id, String dimension_name) {
    super();
    this.sub_alarm_definition_id = sub_alarm_definition_id;
    this.dimension_name = dimension_name;
  }

  public String getSub_alarm_definition_id() {
    return sub_alarm_definition_id;
  }

  public void setSub_alarm_definition_id(String sub_alarm_definition_id) {
    this.sub_alarm_definition_id = sub_alarm_definition_id;
  }

  public String getDimension_name() {
    return dimension_name;
  }

  public void setDimension_name(String dimension_name) {
    this.dimension_name = dimension_name;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((dimension_name == null) ? 0 : dimension_name.hashCode());
    result = prime * result + ((sub_alarm_definition_id == null) ? 0 : sub_alarm_definition_id.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    SubAlarmDefinitionDimensionId other = (SubAlarmDefinitionDimensionId) obj;
    if (dimension_name == null) {
      if (other.dimension_name != null)
        return false;
    } else if (!dimension_name.equals(other.dimension_name))
      return false;
    if (sub_alarm_definition_id == null) {
      if (other.sub_alarm_definition_id != null)
        return false;
    } else if (!sub_alarm_definition_id.equals(other.sub_alarm_definition_id))
      return false;
    return true;
  }
}
